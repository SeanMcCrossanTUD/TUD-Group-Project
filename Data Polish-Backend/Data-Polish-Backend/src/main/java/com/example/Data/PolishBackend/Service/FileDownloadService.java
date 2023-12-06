package com.example.Data.PolishBackend.Service;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.apache.poi.ss.formula.functions.T;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.net.HttpURLConnection;
import java.net.URL;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;

import java.io.IOException;
import java.util.*;

import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.WorkbookFactory;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;


/*
    take jobid as param
    query db to get file details (every column)
    return file details in json format to frontend

    take jobid, fileType(excel,csv) as param
    query db with jobid to get 'datacleaningoutput' value and store it in string 'cleanedFile'
    download the blob (cleaned data) which name equals to 'cleanedFile'  from 'output' container
    check type of the file downloaded from container
    if file type matches with 'fileType' then return that file to frontend
    else convert the file to the 'fileType' and then return to frontend
 */
@Service
public class FileDownloadService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public ResponseEntity<Resource> downloadFile(String jobID, String fileType) {
        try {
            // Retrieve 'datacleaningoutput' from the database and store in cleanedFile
            String sql = "SELECT datacleaningoutput FROM jobsandblobs WHERE jobid = ?";
            String cleanedFile = jdbcTemplate.queryForObject(sql, String.class, jobID);
            ////* in case there's a conversion, use this newCleanedFilename */////
            int lastDotIndex = cleanedFile.lastIndexOf('.');   // the index of the last dot in cleanedFile
            // Extract the substring from the beginning to the last dot
            String newCleanedFilename = cleanedFile.substring(0, lastDotIndex);


            if (cleanedFile == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
            }

            // Construct the URL for downloading the file from Azure Blob Storage
            String blobUrl = String.format("https://fab5storage.blob.core.windows.net/output/%s", cleanedFile);

            // Download the file using HTTP
            Resource download = downloadBlob(blobUrl);

            // Extract file extension from cleanedFile
            String fileExtension = cleanedFile.substring(cleanedFile.lastIndexOf('.'));

            //check if there is a match then just return as it is
            if (fileExtension.equals(fileType)) {
                // If they match, return the file as-is
                HttpHeaders headers = new HttpHeaders();
                headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + cleanedFile);
                return new ResponseEntity<>(download, headers, HttpStatus.OK);
            }

            // If the file extension doesn't match the specified fileType, perform conversion
            else if (".csv".equals(fileType) && ".xlsx".equals(fileExtension)) {
                // Convert XLSX to CSV
                String convertedContent = convertXlsxToCsv(download.getInputStream());
                ByteArrayResource convertedFile = new ByteArrayResource(convertedContent.getBytes(StandardCharsets.UTF_8));

                HttpHeaders headers = new HttpHeaders();
                headers.add(HttpHeaders.CONTENT_TYPE, "text/csv");
                headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + newCleanedFilename + ".csv");

                return new ResponseEntity<>(convertedFile, headers, HttpStatus.OK);
            } else if (".xlsx".equals(fileType) && ".csv".equals(fileExtension)) {
                // Convert CSV to XLSX
                Workbook workbook = convertCsvToXlsx(download.getInputStream());
                ByteArrayResource convertedFile = workbookToByteArrayResource(workbook);

                HttpHeaders headers = new HttpHeaders();
                headers.add(HttpHeaders.CONTENT_TYPE, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
                headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + newCleanedFilename + ".xlsx");

                return new ResponseEntity<>(convertedFile, headers, HttpStatus.OK);
            } else {
                // Unsupported conversion, return as-is
                HttpHeaders headers = new HttpHeaders();
                headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + cleanedFile);
                return new ResponseEntity<>(download, headers, HttpStatus.OK);
            }

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }


        /* prev code
        String sql = "SELECT rawurl, dataprofileoutput, datacleaningoutput FROM jobsandblobs WHERE jobid = ?";

        try {
            // Execute the query to retrieve the file details
            String fileDetails = jdbcTemplate.queryForObject(sql, (rs, rowNum) -> {
                String rawurl = rs.getString("rawurl");
                String dataprofileoutput = rs.getString("dataprofileoutput");
                String datacleaningoutput = rs.getString("datacleaningoutput");
                return "{\"rawurl\":\"" + rawurl + "\", \"dataprofileoutput\":\"" + dataprofileoutput + "\", \"datacleaningoutput\":\"" + datacleaningoutput + "\"}";
            }, jobID);

            // Return the JSON response within a ResponseEntity
            return ResponseEntity.ok(fileDetails);
        } catch (Exception e) {
            // Handle exceptions, e.g., jobID not found, and return an appropriate error response
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Invalid Job ID");
        }

         */
    }

    private Resource downloadBlob(String blobUrl) throws IOException {
        try {
            URL url = new URL(blobUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            // Get the input stream from the connection
            InputStream inputStream = connection.getInputStream();

            // Wrap the input stream in an InputStreamResource
            return new InputStreamResource(inputStream);
        } catch (IOException e) {
            throw e;
        }
    }

    // method for conversion CSV to XLSX using Apache POI
    private Workbook convertCsvToXlsx(InputStream inputStream) throws IOException {

        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Sheet1");

        try (CSVParser csvParser = new CSVParser(new InputStreamReader(inputStream, StandardCharsets.UTF_8),
                CSVFormat.DEFAULT.withHeader())) {
            for (CSVRecord record : csvParser) {
                Row row = sheet.createRow(sheet.getPhysicalNumberOfRows());
                for (int i = 0; i < record.size(); i++) {
                    Cell cell = row.createCell(i);
                    cell.setCellValue(record.get(i));
                }
            }
        }
        return workbook;
    }

    private String convertXlsxToCsv(InputStream inputStream) throws IOException {
        // Implement XLSX to CSV conversion logic using Apache POI
        // This is a simplified example, you may need to adapt it based on your XLSX format
        // Note: The CSV data is assumed to be a simple concatenation of values in this example

        try (Workbook workbook = WorkbookFactory.create(inputStream)) {
            Sheet sheet = workbook.getSheetAt(0);
            StringWriter stringWriter = new StringWriter();
            CSVPrinter csvPrinter = new CSVPrinter(stringWriter, CSVFormat.DEFAULT);

            for (Row row : sheet) {
                List<String> record = new ArrayList<>();
                for (Cell cell : row) {
                    record.add(cell.toString());
                }
                csvPrinter.printRecord(record);
            }

            return stringWriter.toString();
        }
    }

    //method to convert workbook to byte array then create a ByteArrayResource
    private ByteArrayResource workbookToByteArrayResource(Workbook workbook) throws IOException {
        // Convert Workbook to a byte array
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        workbook.write(byteArrayOutputStream);

        // Create a ByteArrayResource from the byte array
        return new ByteArrayResource(byteArrayOutputStream.toByteArray());
    }
}


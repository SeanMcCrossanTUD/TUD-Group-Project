package com.example.Data.PolishBackend.Controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
//import com.azure.storage.queue.QueueClient;
//import com.azure.storage.queue.QueueClientBuilder;
//import com.azure.storage.queue.QueueServiceClient;
//import com.azure.storage.queue.QueueServiceClientBuilder;

import java.io.IOException;

@RestController
@CrossOrigin(origins = {"http://localhost:4200"})
public class FileUploadController {
    //storing the blob connection string in a 'string' variable
    @Value("${azure.storage.connection-string}")
    private String azureConnectionString;

    @PostMapping("/upload-csv")
    public String uploadCSVFile(@RequestParam("file") MultipartFile file)throws IOException {
        // Check if no file is selected to upload
        if (file.isEmpty()) {
            return "Please select a CSV file to upload.";
        }

        // Check if the uploaded file is empty (0 KB in size)
        if (file.getSize() == 0) {
            return "File can not be blank!";
        }
        /*
        return "CSV file uploaded successfully."; */

        // Set up the Azure Blob Service Client
        BlobServiceClient blobServiceClient = new BlobServiceClientBuilder().connectionString(azureConnectionString)
                .buildClient();

        // Set up the Blob Container Client
        BlobContainerClient containerClient = blobServiceClient.getBlobContainerClient("csv");


        try {
            // Create a unique blob name
            String blobName = file.getOriginalFilename();

            // Create a BlobClient
            BlobClient blobClient = containerClient.getBlobClient(blobName);

            // Upload the file to Azure Blob Storage
            blobClient.upload(file.getInputStream(), file.getSize(), true);

            return "CSV file uploaded to Azure Blob Storage successfully.";
        } catch (Exception e) {
            return "An error occurred during the file upload: " + e.getMessage();
        }
    }
}





export class AppSettings {
   
    public static getBaseURL(){
        try{
            // let x=window.location.href;
            // let y=x.split('v2');
            // return y[0];
            return 'http://16.170.150.247:8090/';
        }catch{
            return 'http://localhost:8082/';
        }
       
    }

}
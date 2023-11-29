

export class AppSettings {
   
    public static getBaseURL(){
        try{
            // let x=window.location.href;
            // let y=x.split('v2');
            // return y[0];
            return 'http://localhost:8090/';
        }catch{
            return 'http://localhost:8082/';
        }
       
    }

}
export class constants{
  static helpText_DataNormalization='abc';

}


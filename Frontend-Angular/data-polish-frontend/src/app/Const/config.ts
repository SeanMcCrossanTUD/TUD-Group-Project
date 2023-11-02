

export class AppSettings {
   
    public static getBaseURL(){
        try{
            var x=window.location.href;
            var y=x.split('dev');
            return y[0];
        }catch{
            return window.location.href;
        }
       
    }

}
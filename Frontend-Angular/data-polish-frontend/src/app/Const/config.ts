

export class AppSettings {
   
    public static getBaseURL(){
        var x=window.location.href;
        var y=x.split('dev');
        return y[0];
    }

}
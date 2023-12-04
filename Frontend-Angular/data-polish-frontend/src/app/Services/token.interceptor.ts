

import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {
    constructor(   private cookieService: CookieService){
        
    }
  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    // Get the token from your authentication service or wherever you store it
    
    const token = this.cookieService.get('TOKEN')
    
    // Clone the request and add the Authorization header with the bearer token
    const modifiedRequest = request.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Pass the modified request to the next handler
    return next.handle(modifiedRequest);
  }
}

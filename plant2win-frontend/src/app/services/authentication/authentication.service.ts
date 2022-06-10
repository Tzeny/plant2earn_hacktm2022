import {Injectable} from '@angular/core';
import {Router} from '@angular/router';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {GlobalService} from '../global.service';

@Injectable()
export class AuthenticationService {


    constructor(private http: HttpClient, public _global: GlobalService, private _router: Router) {
    }

    setSession(authResult) {
        const expiresAt = new Date();
        expiresAt.setSeconds(expiresAt.getSeconds() + authResult.expires_in);
      localStorage.setItem('id_token', authResult.auth_token);
      localStorage.setItem('name', authResult.name);
      this._global.name = authResult.name;
      localStorage.setItem('username', authResult.username);
      this._global.username = authResult.username;
    }

    logout() {
        // localStorage.removeItem('id_token');
        localStorage.removeItem('expires_at');
        localStorage.removeItem('username');
        localStorage.removeItem('name');
        localStorage.removeItem('settingsObject');
        this._router.navigate(['/login']);

    }

    login(username, password) {
        const headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');
        return this.http.post(this._global.url + '/login', JSON.stringify({username, password}), {headers: headers});
    }
}

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
    }

    logout() {
        // localStorage.removeItem('id_token');
        localStorage.removeItem('expires_at');

        localStorage.removeItem('username');
        localStorage.removeItem('name');
        localStorage.removeItem('settingsObject');
        this._router.navigate(['/login']);

    }

    isLoggedIn() {
        return (localStorage.getItem('settingsObject') !== null);
    }

    login(username, password) {
        const headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');
        return this.http.post(this._global.url + '/login', JSON.stringify({username, password}), {headers: headers});
    }
}

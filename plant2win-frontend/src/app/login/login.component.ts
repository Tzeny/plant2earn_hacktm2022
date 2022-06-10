import {Component, OnInit, HostListener, ElementRef, ViewChild, DoCheck} from '@angular/core';
import {AuthenticationService} from '../services/authentication/authentication.service';
import {Router} from '@angular/router';
import {MakeToastrService} from '../services/toastr.service';
import {SettingsModel} from '../services/authentication/settings.model';
import {GlobalService} from '../services/global.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  public username: string;
  public password: string;

  constructor(private _authenticationService: AuthenticationService, public _router: Router, private toastr: MakeToastrService, public _global: GlobalService) {

    if (localStorage.getItem('username')) {
      this._router.navigateByUrl('/dashboard');
    }
  }

  Login() {
    this._router.navigateByUrl('/dashboard');
    // First call for login and then call to get the settings object
    this._authenticationService.login(this.username, this.password)
      .subscribe(
        (response: Response) => {
          this._authenticationService.setSession(response);
          // this._authenticationService.getSettings(this.username).subscribe(
          //   (data: SettingsModel) => {
          //   },
          //   error => {
          //     this.toastr.showError(error.error.message, 'Login failed');
          //     console.log(error);
          //   }
          // );
        }, error => {
          this.toastr.showError(error.error.message, 'Login failed');
          console.log(error);
        }
      );
  }

}

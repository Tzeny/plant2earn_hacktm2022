import {Component, ContentChild, DoCheck, ElementRef, ViewChild} from '@angular/core';
import {Location} from '@angular/common';
import {AuthenticationService} from './services/authentication/authentication.service';
// component

import {Router} from '@angular/router';
import {GlobalService} from './services/global.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: []
})
export class AppComponent {
  username = '';
  location: Location;

  constructor(location: Location, private _authenticationService: AuthenticationService,
              private _router: Router, public _global: GlobalService, ) {
    this.location = location;
  }

}

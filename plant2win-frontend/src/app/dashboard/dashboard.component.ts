import { Component, OnInit } from '@angular/core';

import {GlobalService} from '../services/global.service';
import {MakeToastrService} from '../services/toastr.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent  {

  public loading_screen = false;
  public started_upload = false;

  constructor(public _global: GlobalService,  public _toastrService: MakeToastrService) {
    this.started_upload = false;
  }

}

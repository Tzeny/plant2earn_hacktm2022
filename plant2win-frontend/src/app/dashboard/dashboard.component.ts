import {Component, OnInit} from '@angular/core';

import {GlobalService} from '../services/global.service';
import {MakeToastrService} from '../services/toastr.service';
import {MatDialog} from "@angular/material/dialog";
import {DialogComponent} from "../dialog_component/dialog_component";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {

  public loading_screen = false;
  public started_upload = false;

  constructor(public _global: GlobalService, public _toastrService: MakeToastrService, public dialog: MatDialog) {
    this.started_upload = false;
  }

  openDialog() {
    this.dialog.open(DialogComponent);
  }

}

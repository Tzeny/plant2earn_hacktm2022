import {Component, DoCheck, OnInit} from '@angular/core';

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
  public nfts;

  constructor(public _global: GlobalService, public _toastrService: MakeToastrService, public dialog: MatDialog) {
    this.started_upload = false;
    this._global.GetNFTs().subscribe(
      (data) => {
        this.nfts = data;
      }, (error) => {
        console.log(error)
      }
    )
  }


  openDialog(data) {
    this.dialog.open(DialogComponent, {
      data: {
        info: data
      }
    });
  }

  GetLatestPrice(prices) {
    let latest_price = 0;
    for (var price of prices) {
      latest_price = price['price']
    }
    return latest_price
  }

}

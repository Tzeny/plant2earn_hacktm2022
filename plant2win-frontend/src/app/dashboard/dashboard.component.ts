import {Component, DoCheck, OnInit} from '@angular/core';

import {GlobalService} from '../services/global.service';
import {MakeToastrService} from '../services/toastr.service';
import {MatDialog, MatDialogRef} from "@angular/material/dialog";
import {DialogComponent} from "../dialog_component/dialog_component";
import {interval, Subscription} from "rxjs";
import {map, startWith, switchMap} from "rxjs/operators";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  timeInterval: Subscription;
  status: any;

  public loading_screen = false;
  public started_upload = false;
  public nfts;

  public nftIndex = 0;
  public dialogRef: MatDialogRef<DialogComponent>;

  constructor(public _global: GlobalService, public _toastrService: MakeToastrService, public dialog: MatDialog) {
    this.started_upload = false;
    this.getNFTs();
  }

  getNFTs() {
    this._global.GetNFTs().subscribe(
      (data) => {
        this.nfts = data;
      }, (error) => {
        console.log(error)
      }
    )
  }

  ngOnInit() {
    this.timeInterval = interval(5000)
      .pipe(
        startWith(0),
        switchMap(() => this._global.GetNFTs()),
        map(resp => {
          console.log('Got an update!');
          this.nfts = resp;
          if (this.dialogRef !== undefined && this.dialogRef.componentInstance !== null && this.nfts !== undefined) {
            // this.dialogRef.componentInstance.data = {'info': this.nfts[this.nftIndex]};
            console.log(this.dialogRef);
            this.dialogRef.componentInstance.chartLabels = [];
            this.dialogRef.componentInstance.chartData[0]['data'] = [];
            for (var date of this.nfts[this.nftIndex]['price']) {
              this.dialogRef.componentInstance.chartLabels.push(date['timestamp'].split('Z')[1]);
              this.dialogRef.componentInstance.chartData[0]['data'].push(date['price'].split(' ')[0])
            }
          }
        })
      ).subscribe(res => {
      }, err => console.log(err))
  }


  openDialog(data, index) {
    this.nftIndex = index;
    this.dialogRef = this.dialog.open(DialogComponent, {
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

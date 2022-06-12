import {Component, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';
import {Inject} from '@angular/core';
import {ChartConfiguration, ChartDataSets, ChartOptions, ChartType} from 'chart.js';
import {Color, Label} from 'ng2-charts';
import * as pluginDataLabels from 'chartjs-plugin-datalabels';
import {GlobalService} from "../services/global.service";
import {DialogCertificateComponent} from "../dialog_certificate_component/dialog_certificate_component";

@Component({
  selector: 'dialog-selector',
  templateUrl: 'dialog_component.html',
})
export class DialogComponent implements OnInit {
  public username;

  chartData = [
    {
      data: [],
      label: 'µETH Price'
    }
  ];


  chartLabels = [];

  chartColors: Array<any> = [
    { // first color
      backgroundColor: 'rgba(0,0,0,0.2)',
      borderColor: 'green',
      pointBackgroundColor: 'rgba(225,10,24,0.2)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(225,10,24,0.2)'
    }];

  chartOptions = {
    responsive: true
  };

  constructor(public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data: any, private _global: GlobalService) {
  }

  ngOnInit() {
    this.updateChartData();
  }

  updateChartData() {
    this.chartLabels = [];
    for (var date of this.data['info']['price']) {
      this.chartLabels.push(date['timestamp'].split('Z')[1]);
      console.log(date['price'].split(' ')[0]);
      this.chartData[0]['data'].push(date['price'].split(' ')[0])
    }
  }

  BuyForest() {
    this.dialog.open(DialogCertificateComponent);
  }
}

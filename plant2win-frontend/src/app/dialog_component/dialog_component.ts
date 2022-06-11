import {Component, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';
import {Inject} from '@angular/core';
import {ChartConfiguration, ChartDataSets, ChartOptions, ChartType} from 'chart.js';
import {Color, Label} from 'ng2-charts';
import * as pluginDataLabels from 'chartjs-plugin-datalabels';

@Component({
  selector: 'dialog-selector',
  templateUrl: 'dialog_component.html',
})
export class DialogComponent implements OnInit {
  public username;

  chartData = [
    {
      data: [330, 600, 260, 700],
      label: 'Price'
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

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {
  }

  ngOnInit() {
    console.log('On INIT!');
    console.log(this.data);
    this.chartLabels = [];
    for (var date of this.data['info']['price']) {
      this.chartLabels.push(date['timestamp'].split('Z')[1]);
      this.chartLabels.push(date['timestamp'].split('Z')[1]);
    }
  }
}

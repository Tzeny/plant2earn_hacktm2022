import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA} from "@angular/material/dialog";

@Component({
  selector: 'dialog-selector',
  templateUrl: 'dialog_certificate_component.html',
})
export class DialogCertificateComponent implements OnInit {

  public url;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {
  }

  ngOnInit() {
    this.url = this.data['url'];
  }

}

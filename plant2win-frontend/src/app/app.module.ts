import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {HttpClientModule} from '@angular/common/http';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {LoginComponent} from './login/login.component';
import {FormsModule} from '@angular/forms';
import {
  ToastrModule,
  ToastNoAnimation,
  ToastNoAnimationModule
} from 'ngx-toastr';

import {AuthenticationService} from './services/authentication/authentication.service';
import {GlobalService} from './services/global.service';
import {AuthGuard} from './services/authentication/auth.guard';
import {MakeToastrService} from './services/toastr.service';
import {DashboardComponent} from './dashboard/dashboard.component';
import {BorderToolsComponent} from "./border_tools/border.tools.component";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {
  MatButtonModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatSelectModule,
  MatSidenavModule,
  MatCardModule,
  MatTableModule
} from "@angular/material";
import {FlexLayoutModule} from "@angular/flex-layout";
import {DialogComponent} from "./dialog_component/dialog_component";
import {MatDialogModule} from "@angular/material/dialog";
import {ChartsModule} from "ng2-charts";
import {DialogCertificateComponent} from "./dialog_certificate_component/dialog_certificate_component";


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    BorderToolsComponent,
    DialogComponent,
    DialogCertificateComponent
  ],
  imports: [
    FlexLayoutModule,
    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    ChartsModule,
    FormsModule,
    MatSelectModule,
    MatSidenavModule,
    MatCardModule,
    MatTableModule,
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatDialogModule,
    ToastrModule.forRoot({
      timeOut: 2000,
      positionClass: 'toast-top-left',
      preventDuplicates: true,
      maxOpened: 2,
      easing: 'ease-in',
      easeTime: 1,
    }),
  ],
  providers: [
    GlobalService,
    AuthenticationService,
    AuthGuard,
    MakeToastrService
  ],
  entryComponents: [
    DialogComponent,
    DialogCertificateComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}

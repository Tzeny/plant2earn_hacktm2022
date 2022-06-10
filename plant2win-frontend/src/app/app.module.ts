import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import {HttpClientModule} from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import {FormsModule} from '@angular/forms';
import {  ToastrModule,
  ToastNoAnimation,
  ToastNoAnimationModule
} from 'ngx-toastr';

import {AuthenticationService} from './services/authentication/authentication.service';
import {GlobalService} from './services/global.service';
import {AuthGuard} from './services/authentication/auth.guard';
import {MakeToastrService} from './services/toastr.service';
import { DashboardComponent } from './dashboard/dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
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
  bootstrap: [AppComponent]
})
export class AppModule { }

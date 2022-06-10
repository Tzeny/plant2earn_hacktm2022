import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {SettingsModel} from './authentication/settings.model';
import set = Reflect.set;

@Injectable()
export class GlobalService {

  public url: string;
  public name: string;
  public username: string;

  constructor(private _http: HttpClient) {
    this.url = "https://api.xvision.app/";
  }
}


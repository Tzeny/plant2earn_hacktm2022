import {Input, Output, Component, EventEmitter, AfterViewInit, ElementRef, ChangeDetectorRef, Host} from '@angular/core';
import {GlobalService} from '../services/global.service';
import {AuthenticationService} from '../services/authentication/authentication.service';
import set = Reflect.set;

@Component({
    selector: 'app-border-tools',
    templateUrl: './border.tools.component.html',
    styleUrls: ['./border.tools.component.css'],
    providers: []
})
export class BorderToolsComponent {

    name: string;
    // index of the pressed Tool
    pressedTool: number;

    constructor(private _globalService: GlobalService,) {
        this.name = 'Demo Account';
    }

}

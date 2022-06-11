import {Injectable} from '@angular/core';
import {ToastrService} from 'ngx-toastr';

@Injectable()
export class MakeToastrService {

    constructor(private toastr: ToastrService) {

    }

    public showError(message, title) {
        this.toastr.error(message, title);
    }

    public showSuccess(message = 'Your message was saved!', title = 'Thank you!') {
        this.toastr.success(message, title);
    }

    public showInfo(message = 'Your message was saved!', title = 'Thank you!') {
        this.toastr.info(message, title);
    }

}

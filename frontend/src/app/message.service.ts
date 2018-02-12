import { Injectable } from '@angular/core';

@Injectable()
export class MessageService {
    public lastMessage: any;
    public shown = false;

    constructor() { }

    info(message: string): void {
        this.setMessage({
            type: 'info',
            message: message,
        });
    }
    warning(message: string): void {
        this.setMessage({
            type: 'warning',
            message: message,
        });
    }
    error(message: string): void {
        this.setMessage({
            type: 'error',
            message: message,
        });
    }
    setMessage(message: any): void {
        this.lastMessage = message;
        this.shown = true;
        setTimeout(() => this.shown = false, 2000);
    }
}

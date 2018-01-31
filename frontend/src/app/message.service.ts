import { Injectable } from '@angular/core';

@Injectable()
export class MessageService {
    public lastMessage: string = "";
    public shown: boolean = false;

    constructor() { }

    info(message: string): void {
        this.setMessage(message);
    }
    warning(message: string): void {
        this.setMessage(message);
    }
    error(message: string): void {
        this.setMessage(message);
    }
    setMessage(message: string): void {
        this.lastMessage = message;
        this.shown = true;
        setTimeout(() => this.shown = false, 2000);
    }
}

import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable, Subject, Observer } from 'rxjs';
import { delay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  constructor() { }

  private subject: WebSocketSubject<any>;

  connect(url: any): WebSocketSubject<any> {
    if (!this.subject) {
      this.subject = webSocket(url);
    }
    return this.subject;
  }

  send(json: any) {
    this.subject.next(json);
  }
}

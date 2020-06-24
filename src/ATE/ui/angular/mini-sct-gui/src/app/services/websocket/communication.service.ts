import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';
import { Observable, Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { WebsocketService } from './websocket.service';

const DEFAULT_URL = 'ws://localhost:8081/ws';

@Injectable({
  providedIn: 'root'
})
export class CommunicationService {

  message: WebSocketSubject<any>;

  constructor(private readonly wsService: WebsocketService) {
    this.message = (wsService.connect(DEFAULT_URL).pipe(map(
      (response: any) => {
      return response;
    }
    )) as WebSocketSubject<any>);
   }

   send(json: any) {
    this.wsService.send(json);
   }
}

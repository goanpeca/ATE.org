
import { TestBed } from '@angular/core/testing';
import { WebsocketService } from './websocket.service';
import { CommunicationService } from './communication.service';

describe('CommunicationService', () => {
  let service: CommunicationService;
  let websocketService: WebsocketService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CommunicationService, WebsocketService ]
    });
    service = TestBed.get(CommunicationService);
  });

  it('should create an CommunicationService instance', () => {
    expect(service).toBeDefined();
  });

  it('should get message from observable', () => {
    let serviceUnderTest = new CommunicationService(new WebsocketService());
    let test = serviceUnderTest.message.subscribe(msg => console.log('messages should be sent' + msg));
    expect(test).toBeDefined();
  });
});

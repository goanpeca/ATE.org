import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ToggledButtonComponent } from './toggled-button.component';

describe('ToggledButtonComponent', () => {
  let component: ToggledButtonComponent;
  let fixture: ComponentFixture<ToggledButtonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToggledButtonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ToggledButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

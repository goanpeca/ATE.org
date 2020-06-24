import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InformationComponent } from './information.component';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';

describe('informationComponent', () => {
  let component: InformationComponent;
  let fixture: ComponentFixture<InformationComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InformationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InformationComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create information component', () => {
    expect(component).toBeTruthy();
  });

  it('should support heading', () => {
    component.informationConfig.labelText = 'System Information';
    fixture.detectChanges();

    let information = debugElement.query(By.css('h2'));
    let infoElement = information.nativeElement;

    expect(infoElement).toBeTruthy('It should support a heading 2');
    expect(infoElement.innerHTML).toBe('System Information');
  });

  it('should support paragraph', () => {
    component.informationConfig.value = 'Test paragraph';
    fixture.detectChanges();

    let information = debugElement.query(By.css('h3'));
    let infoElement = information.nativeElement;

    expect(infoElement).toBeTruthy('It should support a paragraph');
    expect(infoElement.innerHTML).toBe('Test paragraph');
  });

  it('should get the type of values', () => {
    component.informationConfig.value = 'test';
    let typeOfValue = typeof('test');

    const type = component.typeOf(component.informationConfig.value);

    expect(type).toBe(typeOfValue);
  });
});

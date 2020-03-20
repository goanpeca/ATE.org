import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { SystemState } from '../system-status';
import { SystemControlComponent } from './system-control.component';
import { ToggledButtonComponent } from './toggled-button/toggled-button.component';


describe('SystemControlComponent', () => {
  let component: SystemControlComponent;
  let component1: ToggledButtonComponent;
  let fixture: ComponentFixture<SystemControlComponent>;
  let fixture1: ComponentFixture<ToggledButtonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemControlComponent, ToggledButtonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    fixture1 = TestBed.createComponent(ToggledButtonComponent);
    component1 = fixture1.componentInstance;
    fixture1.detectChanges();
  });

  it('should create system control component', () => {
    expect(component).toBeTruthy();
  });

  it('should create toggled button component', () => {
    expect(component1).toBeTruthy();
  });

  it('should show a disabled unload button when system state is initialized', () => {
    component.systemStatus.state = SystemState.initialized;
    fixture.detectChanges();

    const doc = fixture.nativeElement;

    const unloadButtons = doc.querySelectorAll('#sysControl button');

    let buttonFound = false;
    unloadButtons.forEach(b => {
      if (b.textContent === 'Unload Lot') {
        buttonFound = true;
        expect(b.hasAttribute('disabled')).toBeTruthy('Unload button is expected to be disabled');
      }
    });

    expect(buttonFound).toBeTruthy('Unload button is expected to be on page');
  });
});

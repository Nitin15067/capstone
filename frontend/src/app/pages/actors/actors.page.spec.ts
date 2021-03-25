import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ActorMenuPage } from './actors.page';

describe('ActorMenuPage', () => {
  let component: ActorMenuPage;
  let fixture: ComponentFixture<ActorMenuPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ActorMenuPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ActorMenuPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MovieMenuPage } from './movies.page';

describe('MovieMenuPage', () => {
  let component: MovieMenuPage;
  let fixture: ComponentFixture<MovieMenuPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MovieMenuPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MovieMenuPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { TestBed } from '@angular/core/testing';

import { AnalyseService } from './analyse.service';

describe('AnalyseServiceService', () => {
  let service: AnalyseService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnalyseService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

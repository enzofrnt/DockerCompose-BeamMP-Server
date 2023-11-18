import { Component, OnDestroy } from '@angular/core';
import { ConfigService } from '../services/config.service';
import { Config } from '../models/config';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent implements OnDestroy {

  config!: Config;

  private configSubscription?: Subscription;

  constructor(private configApi : ConfigService)
  {
    configApi.getConfig().subscribe((config) => {
      console.log(config);
      this.config = config;
    });
  }

  ngOnDestroy(): void {
      if (this.configSubscription) {
        this.configSubscription.unsubscribe();
      } 
  }

}

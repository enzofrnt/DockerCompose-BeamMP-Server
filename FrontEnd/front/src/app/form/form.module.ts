import {NgModule, APP_INITIALIZER } from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {MatListModule} from '@angular/material/list';
import {AppRoutingModule} from '../app-routing.module';
import {HttpClientModule} from '@angular/common/http';
import {ReactiveFormsModule} from '@angular/forms'; 
import {MatIconModule} from '@angular/material/icon'; 
import {MatButtonModule} from '@angular/material/button';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations'; 
import {MatInputModule} from '@angular/material/input';
import {MaterialFileInputModule} from 'ngx-material-file-input';
import {MatTableModule} from '@angular/material/table';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatSelectModule} from '@angular/material/select';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDialogModule } from '@angular/material/dialog';




// Components
import {AppComponent} from '../app.component';
import { DownloadDialogComponent } from './download-dialog/download-dialog.component';

@NgModule({
  declarations: [
    DownloadDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatIconModule,
    MatButtonModule,
    BrowserAnimationsModule,
    MatInputModule,
    MaterialFileInputModule,
    MatTableModule,
    MatExpansionModule,
    MatSnackBarModule,
    MatListModule,
    MatSelectModule,
    MatProgressBarModule,
    MatDialogModule
  ]
})
export class FormModule { }

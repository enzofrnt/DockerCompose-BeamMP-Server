import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path : "",
    pathMatch: 'full',
    redirectTo : "product",
  },
  {
    path: "**",
    redirectTo: "product"
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(
      routes,
      {
        anchorScrolling : 'enabled',
        scrollOffset: [0, 32],
      }
    )
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }

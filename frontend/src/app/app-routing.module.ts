import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsersComponent } from './users/users.component';
import { CommunitiesComponent } from './communities/communities.component';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
    { path: 'users', component: UsersComponent },
    { path: 'communities', component: CommunitiesComponent },
];

@NgModule({
    exports: [ RouterModule ],
    imports: [ RouterModule.forRoot(routes) ],
})
export class AppRoutingModule { }

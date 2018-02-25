import { NgModule } from '@angular/core';
import { UsersComponent } from './users/users.component';
import { UserComponent } from './user/user.component';
import { CommunityComponent } from './community/community.component';
import { CommunitiesComponent } from './communities/communities.component';
import { NewYear2018GameComponent } from './new-year-2018-game/new-year-2018-game.component';
import { RouterModule, Routes } from '@angular/router';
import {AboutComponent} from './about/about.component';
import {IndexComponent} from './index/index.component';
import { SecretPageForLactariusComponent } from './secret-page-for-lactarius/secret-page-for-lactarius.component';

const routes: Routes = [
    { path: '', redirectTo: 'index', pathMatch: 'full' },
    { path: 'index', component: IndexComponent },
    { path: 'about', component: AboutComponent },
    { path: 'users', component: UsersComponent },
    { path: 'communities', component: CommunitiesComponent },
    { path: 'user/:username', component: UserComponent },
    { path: 'community/:url_name', component: CommunityComponent },
    { path: 'new_year_2018_game', component:  NewYear2018GameComponent},
    { path: 'secret_page_for_lactarius', component:  SecretPageForLactariusComponent},
];

@NgModule({
    exports: [ RouterModule ],
    imports: [ RouterModule.forRoot(routes) ],
})
export class AppRoutingModule { }

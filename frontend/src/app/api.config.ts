import { HttpClient, HttpHeaders } from '@angular/common/http';


export class ApiConfig {
	public static API_URL = "/api";
	public static USER_API_URL = `${ApiConfig.API_URL}/user`;
	public static USERS_API_URL = `${ApiConfig.API_URL}/users`;

	public static COMMUNITY_API_URL = `${ApiConfig.API_URL}/community`;
	public static COMMUNITIES_API_URL = `${ApiConfig.API_URL}/communities`;

	public static GRAPH_URL = `${ApiConfig.API_URL}/graph`;

	public static NEW_YEAR_2018_GAME_URL = `${ApiConfig.API_URL}/new_year_2018_game`;
	public static NEW_YEAR_2018_GAME_SCOREBOARD_URL = 
		`${ApiConfig.API_URL}/new_year_2018_game/scoreboards/`;
		public static NEW_YEAR_2018_GAME_TOP_URL = 
		`${ApiConfig.API_URL}/new_year_2018_game/top/`;

	public static HTTP_OPTIONS = {
	    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
	};
}

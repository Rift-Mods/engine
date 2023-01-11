public struct Highscore
{
	public string username;

	public int score;

	public int time;

	public int kills;

	public Highscore(string _username, int _score, int _time, int _kills)
	{
		username = _username;
		score = _score;
		time = _time;
		kills = _kills;
	}
}

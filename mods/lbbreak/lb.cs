using System;
using System.Collections;
using UnityEngine;

public class Highscores : MonoBehaviour
{
	[SerializeField]
	private string privateCode;

	[SerializeField]
	private string publicCode;

	private const string webURL = "http://dreamlo.com/lb/";

	private DisplayHighscores highscoreDisplay;

	public Highscore[] highscoresList;

	private static Highscores instance;

	private void Awake()
	{
		highscoreDisplay = GetComponent<DisplayHighscores>();
		instance = this;
	}

	public static void AddNewHighscore(string username, int score, int time, int kills)
	{
		instance.StartCoroutine(instance.UploadNewHighscore(username, score, time, kills));
	}

	internal static void AddNewHighscore(string username, float score, int time, int kills)
	{
		instance.StartCoroutine(instance.UploadNewHighscore(username, score, time, kills));
	}

	private IEnumerator UploadNewHighscore(string username, float score, int time, int kills)
	{
		WWW www = new WWW("http://dreamlo.com/lb/" + privateCode + "/add/" + WWW.EscapeURL(username) + "/" + score + "/" + time + "/" + kills);
		yield return www;
		if (string.IsNullOrEmpty(www.error))
		{
			MonoBehaviour.print("Upload Successful");
			DownloadHighscores();
		}
		else
		{
			MonoBehaviour.print("Error uploading: " + www.error);
		}
	}

	private IEnumerator UploadNewHighscore(string username, int score, int time, int kills)
	{
		WWW www = new WWW("http://dreamlo.com/lb/" + privateCode + "/add/" + WWW.EscapeURL(username) + "/" + score + "/" + time + "/" + kills);
		yield return www;
		if (string.IsNullOrEmpty(www.error))
		{
			MonoBehaviour.print("Upload Successful");
			DownloadHighscores();
		}
		else
		{
			MonoBehaviour.print("Error uploading: " + www.error);
		}
	}

	public void DownloadHighscores()
	{
		StartCoroutine("DownloadHighscoresFromDatabase");
	}

	private IEnumerator DownloadHighscoresFromDatabase()
	{
		WWW www = new WWW("http://dreamlo.com/lb/" + publicCode + "/pipe/");
		yield return www;
		if (string.IsNullOrEmpty(www.error))
		{
			FormatHighscores(www.text);
		}
		else
		{
			MonoBehaviour.print("Error Downloading: " + www.error);
		}
	}

	private void FormatHighscores(string textStream)
	{
		string[] array = textStream.Split(new char[1] { '\n' }, StringSplitOptions.RemoveEmptyEntries);
		highscoresList = new Highscore[array.Length];
		for (int i = 0; i < array.Length; i++)
		{
			string[] array2 = array[i].Split(new char[1] { '|' });
			string username = array2[0];
			int score = int.Parse(array2[1]);
			int time = int.Parse(array2[2]);
			int kills = int.Parse(array2[3]);
			highscoresList[i] = new Highscore(username, score, time, kills);
            Debug.Log(privateCode);
		}
        Debug.Log(privateCode);
        // highscoresList[array.Length - 2] = new Highscore(privateCode, -1, 0, 0);
        // highscoresList[array.Length - 1] = new Highscore(publicCode, -2, 0, 0);
		highscoreDisplay.OnHighscoresDownloaded(highscoresList);
	}
}

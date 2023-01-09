using System;
using TMPro;
using UnityEngine;

// Token: 0x02000006 RID: 6
public class GauntletManager : MonoBehaviour
{
	// Token: 0x0600000C RID: 12 RVA: 0x00002514 File Offset: 0x00000714
	private void Start()
	{
		if (PlayerPrefs.GetFloat("score") != 0f && PlayerPrefs.GetFloat("score") != float.PositiveInfinity && PlayerPrefs.GetFloat("highscoreTime") != 0f)
		{
			GauntletManager.highscore = PlayerPrefs.GetFloat("score");
			Highscores.AddNewHighscore(PlayerPrefs.GetString("Username"), Mathf.RoundToInt(GauntletManager.highscore), Mathf.RoundToInt(PlayerPrefs.GetFloat("highscoreTime")), PlayerPrefs.GetInt("highscoreKills"));
		}
	}

	// Token: 0x0600000D RID: 13 RVA: 0x000025A0 File Offset: 0x000007A0
	private void Update()
	{
		if (this.timerstarted)
		{
			this.curTime += Time.deltaTime;
		}
		this.oneWayShield.SetActive(!this.timerstarted);
		TMP_Text[] array = this.updateText;
		for (int i = 0; i < array.Length; i++)
		{
			array[i].text = GauntletManager.Round(this.curTime, 2).ToString() + "s";
		}
		this.highscore_text.text = "funny text :)";
		this.score.text = "editing 101 :D";
	}

	// Token: 0x0600000E RID: 14 RVA: 0x00002670 File Offset: 0x00000870
	public static float Round(float value, int digits)
	{
		float num = Mathf.Pow(10f, (float)digits);
		return Mathf.Round(value * num) / num;
	}

	// Token: 0x0600000F RID: 15 RVA: 0x00002694 File Offset: 0x00000894
	public void ResetTimer()
	{
		this.curTime = 0f;
		this.timerstarted = false;
	}

	// Token: 0x06000010 RID: 16 RVA: 0x000026A8 File Offset: 0x000008A8
	public void StartTimer()
	{
		this.ResetTimer();
		if (this.timerstarted)
		{
			this.timerstarted = false;
			Health[] array = this.targets;
			for (int i = 0; i < array.Length; i++)
			{
				array[i].ResetTarget();
			}
			return;
		}
		this.timerstarted = true;
	}

	// Token: 0x06000011 RID: 17 RVA: 0x000026F8 File Offset: 0x000008F8
	public void StopTimer()
	{
		this.timerstarted = false;
		int num = 0;
		foreach (Health health in this.targets)
		{
			if (health.hit)
			{
				num++;
			}
			health.ResetTarget();
		}
		float value = 1000f / GauntletManager.Round(this.curTime, 2) + (float)(num * 3);
		this.playerScore = GauntletManager.Round(value, 2);
		if (this.playerScore > GauntletManager.highscore)
		{
			GauntletManager.highscore = this.playerScore;
			PlayerPrefs.SetFloat("score", GauntletManager.highscore);
			PlayerPrefs.SetFloat("highscoreTime", this.curTime);
			PlayerPrefs.SetInt("highscoreKills", num);
			Highscores.AddNewHighscore(PlayerPrefs.GetString("Username"), Mathf.RoundToInt(GauntletManager.highscore), Mathf.RoundToInt(this.curTime), num);
		}
	}

	// Token: 0x04000009 RID: 9
	public TMP_Text[] updateText;

	// Token: 0x0400000A RID: 10
	public TMP_Text highscore_text;

	// Token: 0x0400000B RID: 11
	public TMP_Text score;

	// Token: 0x0400000C RID: 12
	public Health[] targets;

	// Token: 0x0400000D RID: 13
	private float curTime;

	// Token: 0x0400000E RID: 14
	private bool timerstarted;

	// Token: 0x0400000F RID: 15
	public GameObject oneWayShield;

	// Token: 0x04000010 RID: 16
	public float playerScore;

	// Token: 0x04000011 RID: 17
	public static float highscore;
}

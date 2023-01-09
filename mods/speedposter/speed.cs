using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

// Token: 0x02000013 RID: 19
public class Poster : MonoBehaviour
{
	// Token: 0x0600004F RID: 79 RVA: 0x00003B1B File Offset: 0x00001D1B
	private void Start()
	{
		base.StartCoroutine("ChangePhoto");
		this.index = UnityEngine.Random.Range(0, this.sprite.Length);
	}

	// Token: 0x06000050 RID: 80 RVA: 0x00003B40 File Offset: 0x00001D40
	public IEnumerator ChangePhoto()
	{
		if (this.index == 14)
		{
			this.index = 0;
		}
		else
		{
			this.index++;
		}
		this.image.sprite = this.sprite[this.index];
		yield return new WaitForSeconds(0.1f);
		base.StartCoroutine("ChangePhoto");
		yield break;
	}

	// Token: 0x0400004E RID: 78
	public Sprite[] sprite;

	// Token: 0x0400004F RID: 79
	public float timeBetweenPosters;

	// Token: 0x04000050 RID: 80
	public Image image;

	// Token: 0x04000051 RID: 81
	private int index;
}

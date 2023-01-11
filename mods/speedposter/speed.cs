using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class Poster : MonoBehaviour
{
	public Sprite[] sprite;

	public float timeBetweenPosters;

	public Image image;

	private int index;

	private void Start()
	{
		StartCoroutine("ChangePhoto");
		index = Random.Range(0, sprite.Length);
	}

	public IEnumerator ChangePhoto()
	{
		if (index == 14)
		{
			index = 0;
		}
		else
		{
			index++;
		}
		image.sprite = sprite[index];
		yield return new WaitForSeconds(0.1f);
		StartCoroutine("ChangePhoto");
	}
}

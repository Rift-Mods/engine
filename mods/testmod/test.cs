using System;
using UnityEngine;

// Token: 0x02000073 RID: 115
public class DoubleJump : MonoBehaviour
{
	// Token: 0x06000204 RID: 516 RVA: 0x0000A8B8 File Offset: 0x00008AB8
	private void Start()
	{
		this.controller = base.GetComponent<PlayerController>();
		this.wallrun = base.GetComponent<WallRun>();
		this.jumpsLeft = this.extraJumps;
	}

	// Token: 0x06000205 RID: 517 RVA: 0x0000A8E0 File Offset: 0x00008AE0
	private void Update()
	{
		this.rb = this.controller.rb;
		if (Input.GetKeyDown(base.GetComponent<PlayerInput>().Jump) && this.jumpsLeft > 0 && !this.controller.IsGrounded && !this.wallrun.WallNear)
		{
			this.DJump();
		}
		if (this.controller.IsGrounded)
		{
			this.jumpsLeft = this.extraJumps;
		}
	}

	// Token: 0x06000206 RID: 518 RVA: 0x0000A952 File Offset: 0x00008B52
	public void ResetDoubleJump()
	{
		this.jumpsLeft = this.extraJumps;
	}

	// Token: 0x06000207 RID: 519 RVA: 0x0000A960 File Offset: 0x00008B60
	public void EmptyJumps()
	{
		this.jumpsLeft = 0;
	}

	// Token: 0x06000208 RID: 520 RVA: 0x0000A96C File Offset: 0x00008B6C
	private void DJump()
	{
		if (this.rb.velocity.y < 0f)
		{
			this.rb.velocity = new Vector3(this.rb.velocity.x, this.rb.velocity.y * 0.1f, this.rb.velocity.z);
		}
		this.rb.velocity = new Vector3(this.rb.velocity.x, this.rb.velocity.y + this.jumpForce, this.rb.velocity.z);
		base.GetComponent<CameraMotion>().BobOnce(this.shakeMag);
		base.GetComponent<AudioSource>().pitch = UnityEngine.Random.Range(base.GetComponent<AudioSource>().pitch - 0.1f, base.GetComponent<AudioSource>().pitch + 0.1f);
		base.GetComponent<AudioSource>().PlayOneShot(this.doubleJumpThrustSound);
	}

	// Token: 0x040002BE RID: 702
	public float jumpForce;

	// Token: 0x040002BF RID: 703
	public int extraJumps;

	// Token: 0x040002C0 RID: 704
	public float shakeMag;

	// Token: 0x040002C1 RID: 705
	public AudioClip doubleJumpThrustSound;

	// Token: 0x040002C2 RID: 706
	private PlayerController controller;

	// Token: 0x040002C3 RID: 707
	private WallRun wallrun;

	// Token: 0x040002C4 RID: 708
	private Rigidbody rb;

	// Token: 0x040002C5 RID: 709
	public int jumpsLeft;
}

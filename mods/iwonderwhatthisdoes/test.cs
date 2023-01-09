using System;
using UnityEngine;

// Token: 0x02000040 RID: 64
public class DualWieldManager : MonoBehaviour, IItem
{
	// Token: 0x17000024 RID: 36
	// (get) Token: 0x06000115 RID: 277 RVA: 0x00007A58 File Offset: 0x00005C58
	public string ItemName
	{
		get
		{
			return this._name;
		}
	}

	// Token: 0x06000116 RID: 278 RVA: 0x00007A60 File Offset: 0x00005C60
	public void OnEquip()
	{
		throw new NotImplementedException();
	}

	// Token: 0x06000117 RID: 279 RVA: 0x00007A67 File Offset: 0x00005C67
	public void OnUnequip()
	{
		throw new NotImplementedException();
	}

	// Token: 0x06000118 RID: 280 RVA: 0x00007A6E File Offset: 0x00005C6E
	private void Start()
	{
		this.gun1.canUse = false;
		this.gun2.canUse = false;
		this.l = base.GetComponentInParent<Loadout>();
	}

	// Token: 0x06000119 RID: 281 RVA: 0x00007A94 File Offset: 0x00005C94
	private void Update()
	{
		this.gun1.canUse = true;
		this.gun2.canUse = true;
		if (Input.GetMouseButtonDown(0))
		{
			this.gun1.OnShoot();
            this.gun2.OnShoot();
		}
		if (Input.GetMouseButtonDown(1))
		{
			this.gun2.OnShoot();
            this.gun1.OnShoot();
		}
		this.l.SetWeaponAndAmmoText(this.gun1.clipAmount.ToString() + "/" + this.gun2.clipAmount.ToString(), this._name);
	}

	// Token: 0x04000188 RID: 392
	public Gun gun1;

	// Token: 0x04000189 RID: 393
	public Gun gun2;

	// Token: 0x0400018A RID: 394
	public string _name;

	// Token: 0x0400018B RID: 395
	private Loadout l;
}

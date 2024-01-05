"""
Generic ranged weapon class that stores basic weapon info and shooting function
By: Nick Petruccelli
Last Modified: 08/10/2023
"""

from typing import Tuple

from Scripts.Player.Weapons.weapon import Weapon


class RangedWeapon(Weapon):
    emit_offset: Tuple[float, float]

    bullet_force: float = 25.0
    rate_of_fire = 4.0

    _last_fire_time: float
    _damage_final: float
    _crit_chance_final: float

    def __init__(self, player_stats):
        super().__init__(
            weapon_name="Ranged",
            base_damage=25.0,
            crit_chance=0.05,
            crit_mult=2.0
        )

        self._last_fire_time = - 1 / self.rate_of_fire
        self._damage_final = self.base_damage * player_stats.damage_mult
        self._crit_chance_final = self.crit_chance + player_stats.crit_chance

    def update(self):
        raise NotImplementedError

    #     if (Input.GetButton("Fire1") && (lastFireTime + fireDelay < Time.time))
    #     {
    #         Shoot();
    #         lastFireTime = Time.time;
    #     }
    #
    #

    def fire_projectile(self):
        raise NotImplementedError
    # {
    #     // Instantiate bullet and access its rigid body
    #     GameObject bullet = Instantiate(bulletPreFab, firePoint.position, firePoint.rotation);
    #     Rigidbody2D rb = bullet.GetComponent<Rigidbody2D>();
    #     Bullet bulletScript = bullet.GetComponent<Bullet>();
    #
    #     // Determine if bullet is going to crit and adjust damage if it does
    #     float random = Random.Range(0,1);
    #     float damageTemp = damageFinal;
    #     if (critChance >= random)
    #     {
    #         damageFinal = damageFinal * critMultiplier;
    #     }
    #
    #     // Apply damage to bullet and move it foward
    #     bulletScript.SetDamage(damageFinal);
    #     rb.AddForce(firePoint.up * bulletForce, ForceMode2D.Impulse);
    #
    #     // Reset damage back to non crit damage
    #     damageFinal = damageTemp;

class Bullet:
    def __init__(self, damage: float):
        self.hit_effect = None
        self.damage = damage

    def deal_damage(self):

        ...
        #     void OnCollisionEnter2D(Collision2D collision)
        #     {
        #         if(collision.gameObject.tag == "Enemy")
        #         {
        #             Enemy enemyStats = collision.gameObject.GetComponent<Enemy>();
        #             enemyStats.takeDamage(damage);
        #         }
        #
        #         Instantiate(hitEffect, transform.position, Quaternion.identity);
        #         Destroy(gameObject);
        #     }


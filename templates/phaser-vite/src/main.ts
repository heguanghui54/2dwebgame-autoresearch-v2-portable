import Phaser from "phaser";

const WIDTH = 1280;
const HEIGHT = 720;
const WORLD_WIDTH = 2560;

class TemplateScene extends Phaser.Scene {
  private player!: Phaser.Types.Physics.Arcade.SpriteWithDynamicBody;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private restartKey!: Phaser.Input.Keyboard.Key;
  private attackKey!: Phaser.Input.Keyboard.Key;
  private goalReached = false;

  constructor() {
    super("template");
  }

  create() {
    this.physics.world.setBounds(0, 0, WORLD_WIDTH, HEIGHT);

    const graphics = this.add.graphics();
    graphics.fillStyle(0xffffff, 1);
    graphics.fillRect(0, 0, 64, 32);
    graphics.generateTexture("platform", 64, 32);
    graphics.clear();
    graphics.fillStyle(0xffffff, 1);
    graphics.fillRoundedRect(0, 0, 42, 72, 10);
    graphics.generateTexture("hero", 42, 72);
    graphics.destroy();

    this.add.rectangle(WORLD_WIDTH / 2, HEIGHT / 2, WORLD_WIDTH, HEIGHT, 0x123447);
    this.add.rectangle(WORLD_WIDTH / 2, 610, WORLD_WIDTH, 220, 0x194f59).setAlpha(0.45);

    for (let x = 160; x < WORLD_WIDTH; x += 420) {
      this.add.circle(x, 120 + ((x / 420) % 3) * 70, 5, 0x7ee8df, 0.7);
      this.add.rectangle(x + 100, 190, 140, 18, 0x7cd6c9, 0.22);
    }

    const platforms = this.physics.add.staticGroup();
    platforms.create(360, 650, "platform").setDisplaySize(720, 48).refreshBody();
    platforms.create(920, 520, "platform").setDisplaySize(320, 40).refreshBody();
    platforms.create(1380, 430, "platform").setDisplaySize(340, 40).refreshBody();
    platforms.create(1860, 520, "platform").setDisplaySize(360, 40).refreshBody();
    platforms.create(2320, 650, "platform").setDisplaySize(480, 48).refreshBody();

    platforms.getChildren().forEach((child) => {
      const body = child as Phaser.Physics.Arcade.Image;
      body.setTint(0x274b55);
    });

    this.player = this.physics.add.sprite(80, 560, "hero");
    this.player.setDisplaySize(42, 72);
    this.player.setTint(0xf3d36b);
    this.player.setCollideWorldBounds(true);
    this.player.body.setSize(34, 68).setOffset(4, 4);

    this.physics.add.collider(this.player, platforms);

    const door = this.add.rectangle(WORLD_WIDTH - 80, 574, 58, 144, 0x62e7d4, 0.9);
    this.physics.add.existing(door, true);
    this.physics.add.overlap(this.player, door as Phaser.Types.Physics.Arcade.GameObjectWithBody, () => {
      this.goalReached = true;
      this.add.text(this.cameras.main.scrollX + WIDTH / 2, 220, "Victory - press R", {
        color: "#f5e8b0",
        fontSize: "34px",
        fontFamily: "system-ui, sans-serif"
      }).setOrigin(0.5).setScrollFactor(0);
    });

    this.cameras.main.setBounds(0, 0, WORLD_WIDTH, HEIGHT);
    this.cameras.main.startFollow(this.player, true, 0.08, 0.08);

    this.cursors = this.input.keyboard!.createCursorKeys();
    this.restartKey = this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.R);
    this.attackKey = this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.J);

    this.add.text(24, 20, "Arrow keys move/jump, J attacks, R restarts", {
      color: "#e7fbff",
      fontSize: "18px",
      fontFamily: "system-ui, sans-serif"
    }).setScrollFactor(0);
  }

  update() {
    if (Phaser.Input.Keyboard.JustDown(this.restartKey)) {
      this.scene.restart();
      return;
    }

    const speed = this.goalReached ? 0 : 270;
    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-speed);
      this.player.setFlipX(true);
    } else if (this.cursors.right.isDown) {
      this.player.setVelocityX(speed);
      this.player.setFlipX(false);
    } else {
      this.player.setVelocityX(0);
    }

    if (this.cursors.up.isDown && this.player.body.blocked.down && !this.goalReached) {
      this.player.setVelocityY(-570);
    }

    if (Phaser.Input.Keyboard.JustDown(this.attackKey)) {
      this.cameras.main.zoomTo(1.14, 180, Phaser.Math.Easing.Sine.Out, true, (_camera, progress) => {
        if (progress === 1) {
          this.cameras.main.zoomTo(1, 260, Phaser.Math.Easing.Sine.InOut, true);
        }
      });
    }
  }
}

new Phaser.Game({
  type: Phaser.AUTO,
  parent: "game",
  width: WIDTH,
  height: HEIGHT,
  backgroundColor: "#071c26",
  physics: {
    default: "arcade",
    arcade: {
      gravity: { x: 0, y: 1400 },
      debug: false
    }
  },
  scene: TemplateScene,
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  }
});

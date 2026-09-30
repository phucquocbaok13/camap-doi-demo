<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Hungry Shark HTML5 Demo</title>
    <style>
        body { margin: 0; overflow: hidden; background: #001e3d; font-family: sans-serif; }
        canvas { display: block; background: linear-gradient(to bottom, #0077be, #001e3d); }
        #ui { position: absolute; top: 10px; left: 10px; color: white; font-size: 18px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="ui">
        <div>Máu: <span id="health">100</span>%</div>
        <div>Điểm: <span id="score">0</span></div>
        <small style="color: #aaa;">Dùng chuột để hướng dẫn cá bơi | Giữ phím SPACE để Tăng tốc (Boost)</small>
    </div>
    <canvas id="gameCanvas"></canvas>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let mouse = { x: canvas.width / 2, y: canvas.height / 2 };
let isBoosting = false;
let score = 0;

window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
window.addEventListener('keydown', (e) => { if (e.code === 'Space') isBoosting = true; });
window.addEventListener('keyup', (e) => { if (e.code === 'Space') isBoosting = false; });

// Đối tượng Cá Mập
class Shark {
    constructor() {
        this.x = canvas.width / 2;
        this.y = canvas.height / 2;
        this.radius = 25;
        this.angle = 0;
        this.speed = 3;
        this.health = 100;
    }

    update() {
        let dx = mouse.x - this.x;
        let dy = mouse.y - this.y;
        this.angle = Math.atan2(dy, dx);

        let currentSpeed = isBoosting ? this.speed * 2.5 : this.speed;
        
        if (Math.hypot(dx, dy) > 10) {
            this.x += Math.cos(this.angle) * currentSpeed;
            this.y += Math.sin(this.angle) * currentSpeed;
        }

        // Máu giảm dần theo thời gian
        this.health -= 0.05;
        if (this.health <= 0) this.health = 0;
        
        document.getElementById('health').innerText = Math.ceil(this.health);
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);

        // Vẽ thân cá mập
        ctx.fillStyle = isBoosting ? '#ff4d4d' : '#4a90e2';
        ctx.beginPath();
        ctx.ellipse(0, 0, this.radius * 1.5, this.radius, 0, 0, Math.PI * 2);
        ctx.fill();

        // Mắt
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(10, -5, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(12, -5, 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }
}

// Đối tượng Con Mồi
class Fish {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.radius = 10;
        this.color = '#f5a623';
        this.vx = (Math.random() - 0.5) * 2;
        this.vy = (Math.random() - 0.5) * 2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
    }
}

const shark = new Shark();
const fishes = Array.from({ length: 15 }, () => new Fish());

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (shark.health > 0) {
        shark.update();
        shark.draw();

        fishes.forEach((fish, index) => {
            fish.update();
            fish.draw();

            // Va chạm (Ăn mồi)
            let dist = Math.hypot(shark.x - fish.x, shark.y - fish.y);
            if (dist < shark.radius + fish.radius) {
                fishes.splice(index, 1);
                fishes.push(new Fish()); // Sinh cá mới
                shark.health = Math.min(100, shark.health + 15); // Hồi máu
                score += 10;
                document.getElementById('score').innerText = score;
            }
        });

        requestAnimationFrame(animate);
    } else {
        ctx.fillStyle = 'white';
        ctx.font = '40px sans-serif';
        ctx.fillText('GAME OVER!', canvas.width / 2 - 130, canvas.height / 2);
    }
}

animate();
</script>
</body>
</html>

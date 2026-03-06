const canvas = document.getElementById("lightRays");

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);

camera.position.z = 6;

const renderer = new THREE.WebGLRenderer({
  canvas: canvas,
  alpha: true,
  antialias: true
});

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

const rays = [];

const rayCount = 40;

function createRay() {

  const geometry = new THREE.PlaneGeometry(
    0.6 + Math.random() * 1.8,
    12,
    1,
    1
  );

  const material = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.04 + Math.random() * 0.05,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  });

  const ray = new THREE.Mesh(geometry, material);

  ray.position.x = (Math.random() - 0.5) * 12;
  ray.position.y = -6 - Math.random() * 3;
  ray.position.z = (Math.random() - 0.5) * 3;

  ray.rotation.z = (Math.random() - 0.5) * 0.6;

  ray.userData.speed = 0.004 + Math.random() * 0.008;

  scene.add(ray);
  rays.push(ray);
}

for (let i = 0; i < rayCount; i++) {
  createRay();
}

let mouseX = 0;
let mouseY = 0;

document.addEventListener("mousemove", (e) => {

  mouseX = (e.clientX / window.innerWidth - 0.5) * 0.6;
  mouseY = (e.clientY / window.innerHeight - 0.5) * 0.6;

});

function animate() {

  requestAnimationFrame(animate);

  rays.forEach(ray => {

    ray.position.y += ray.userData.speed;

    if (ray.position.y > 7) {
      ray.position.y = -7;
    }

  });

  camera.position.x += (mouseX - camera.position.x) * 0.03;
  camera.position.y += (-mouseY - camera.position.y) * 0.03;

  renderer.render(scene, camera);

}

animate();

window.addEventListener("resize", () => {

  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(window.innerWidth, window.innerHeight);

});

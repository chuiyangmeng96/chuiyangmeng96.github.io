document.documentElement.classList.add("js");

const revealElements = Array.from(document.querySelectorAll(".reveal"));
const navLinks = Array.from(document.querySelectorAll(".site-nav a"));
const sectionMap = navLinks
  .map((link) => {
    const section = document.querySelector(link.getAttribute("href"));
    return section ? { link, section } : null;
  })
  .filter(Boolean);

revealElements.forEach((element) => element.classList.add("is-visible"));

if ("IntersectionObserver" in window) {
  const navObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const pair = sectionMap.find((item) => item.section === entry.target);
        if (!pair) return;

        if (entry.isIntersecting) {
          navLinks.forEach((link) => link.classList.remove("active"));
          pair.link.classList.add("active");
        }
      });
    },
    { threshold: 0.35, rootMargin: "-20% 0px -35% 0px" }
  );

  sectionMap.forEach((item) => navObserver.observe(item.section));
}

const yearNode = document.getElementById("year");
if (yearNode) yearNode.textContent = String(new Date().getFullYear());

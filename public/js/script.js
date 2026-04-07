// 页面加载完成后执行
(function() {
    // 隐藏加载动画
    setTimeout(function() {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.classList.add('hidden');
        }
    }, 800);
    
    // 触发页面动画
    console.log('开始触发动画...');
    
    // 触发标题动画
    const title = document.querySelector('h1.mb-5');
    console.log('标题元素:', title);
    if (title) {
        console.log('添加标题动画');
        setTimeout(() => {
            title.classList.add('fade-in-up');
            console.log('标题动画已添加');
        }, 100);
    }
    
    // 触发文章卡片动画
    const cards = document.querySelectorAll('.home-post-card, .web-card, .pwn-card, .misc-card, .crypto-card, .reverse-card, .algorithm-card');
    console.log('文章卡片数量:', cards.length);
    cards.forEach((card, index) => {
        console.log('添加卡片动画:', index);
        setTimeout(() => {
            card.classList.add('fade-in-up');
            console.log('卡片动画已添加:', index);
        }, 300 + (index * 200));
    });
    
    // 触发警告框动画
    const alert = document.querySelector('.alert');
    console.log('警告框元素:', alert);
    if (alert) {
        console.log('添加警告框动画');
        setTimeout(() => {
            alert.classList.add('fade-in-up');
            console.log('警告框动画已添加');
        }, 300);
    }
    
    console.log('动画触发逻辑执行完成');


    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // 表单提交前的验证
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('请填写所有必填字段');
            }
        });
    });

    // 实时验证密码强度
    const passwordField = document.querySelector('input[type="password"]');
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            const strengthIndicator = document.createElement('div');
            strengthIndicator.className = 'mt-2';
            
            if (password.length < 6) {
                strengthIndicator.textContent = '密码强度: 弱';
                strengthIndicator.className = 'mt-2 text-danger';
            } else if (password.length < 10) {
                strengthIndicator.textContent = '密码强度: 中';
                strengthIndicator.className = 'mt-2 text-warning';
            } else {
                strengthIndicator.textContent = '密码强度: 强';
                strengthIndicator.className = 'mt-2 text-success';
            }

            const existingIndicator = this.parentElement.querySelector('.mt-2');
            if (existingIndicator) {
                existingIndicator.replaceWith(strengthIndicator);
            } else {
                this.parentElement.appendChild(strengthIndicator);
            }
        });
    }

    // 为卡片添加悬停效果
    const allCards = document.querySelectorAll('.card');
    allCards.forEach(card => {
        // 移除悬停效果，避免影响点击
    });

    // 为按钮添加点击效果
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // 创建点击效果
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            // 移除点击效果
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // 为导航链接添加交互效果
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            // 移除悬停效果，避免影响点击
        });
        link.addEventListener('mouseleave', function() {
            // 移除悬停效果，避免影响点击
        });
    });

    // 为评论添加动画效果
    const comments = document.querySelectorAll('.comment');
    comments.forEach((comment, index) => {
        setTimeout(() => {
            comment.style.opacity = '1';
            comment.style.transform = 'translateX(0)';
        }, 100 * index);
    });

    // 为搜索框添加交互效果
    const searchInput = document.querySelector('.search-input');
    const searchButton = document.querySelector('.search-button');
    console.log('搜索输入框:', searchInput);
    console.log('搜索按钮:', searchButton);
    if (searchInput && searchButton) {
        console.log('搜索元素找到，绑定事件');
        searchInput.addEventListener('focus', function() {
            this.style.width = '110%';
            this.style.boxShadow = '0 0 0 0.3rem rgba(67, 97, 238, 0.2)';
        });
        searchInput.addEventListener('blur', function() {
            this.style.width = '100%';
            this.style.boxShadow = 'none';
        });
        
        // 为搜索按钮添加点击事件
        searchButton.addEventListener('click', function() {
            console.log('搜索按钮被点击');
            const searchTerm = searchInput.value.trim().toLowerCase();
            console.log('搜索词:', searchTerm);
            const postCards = document.querySelectorAll('.card.home-post-card, .card.web-card, .card.pwn-card, .card.misc-card, .card.crypto-card, .card.reverse-card, .card.algorithm-card');
            console.log('找到的文章卡片数量:', postCards.length);
            
            postCards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const content = card.querySelector('.card-text').textContent.toLowerCase();
                console.log('文章标题:', title);
                console.log('文章内容:', content);
                console.log('标题包含搜索词:', title.includes(searchTerm));
                console.log('内容包含搜索词:', content.includes(searchTerm));
                
                if (title.includes(searchTerm) || content.includes(searchTerm)) {
                    card.style.display = 'block';
                    console.log('显示文章:', title);
                } else {
                    card.style.display = 'none';
                    console.log('隐藏文章:', title);
                }
            });
        });
        
        // 为搜索输入框添加回车事件
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                console.log('回车键被按下');
                searchButton.click();
            }
        });
    } else {
        console.log('搜索元素未找到');
    }

    // 为标签添加交互效果
    const tags = document.querySelectorAll('.tag');
    tags.forEach(tag => {
        tag.addEventListener('click', function() {
            this.style.transform = 'scale(1.1)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
        });
    });

    // 为分页链接添加交互效果
    const pageLinks = document.querySelectorAll('.pagination .page-link');
    pageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href !== '#') {
                // 添加加载动画
                const loader = document.getElementById('loader');
                if (loader) {
                    loader.classList.remove('hidden');
                }
                // 延迟跳转，让用户看到加载动画
                setTimeout(() => {
                    window.location.href = href;
                }, 300);
            }
        });
    });

    // 为社交媒体链接添加交互效果
    const socialLinks = document.querySelectorAll('.social-links a');
    socialLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href !== '#') {
                window.open(href, '_blank');
            }
        });
    });

    // 为文章卡片添加阅读时间估算
    const postContents = document.querySelectorAll('.card-text');
    postContents.forEach(content => {
        const text = content.textContent;
        const words = text.split(' ').length;
        const readingTime = Math.ceil(words / 200); // 假设每分钟阅读200字
        const readingTimeElement = document.createElement('p');
        readingTimeElement.className = 'reading-time mt-2';
        readingTimeElement.innerHTML = `<i class="fas fa-clock mr-1"></i> 阅读时间: ${readingTime} 分钟`;
        content.parentElement.appendChild(readingTimeElement);
    });
})();
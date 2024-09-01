<script lang = "ts">

export default {
    setup() {
        return;
    }
}


</script>

<template>

    <div class="menu">
        <div class="menu_buttons">

            <RouterLink to="/">
                <div class="menu_button">
                    <img style="object-fit: contain;" src="./../assets/img/diamond.svg" alt="diamond">
                    <p>Home</p>
                </div>
            </RouterLink>

            <RouterLink to="/earn">
                <div class="menu_button">
                    <img style="object-fit: contain;" src="./../assets/img/money.svg" alt="money">
                    <p>Earn</p>
                </div>
            </RouterLink>

            <RouterLink to="/upgrades">
                <div class="menu_button">
                    <img style="object-fit: contain;" src="./../assets/img/energy.svg" alt="energy">
                    <p>Upgrade</p>
                </div>
            </RouterLink>

            <RouterLink to="/shop">
                <div class="menu_button">
                    <img style="object-fit: contain;" src="./../assets/img/shop.svg" alt="shop">
                    <p>Shop</p>
                </div>
            </RouterLink>

            <RouterLink to="/profile">
                <div class="menu_button">
                    <img style="object-fit: contain;" src="./../assets/img/profile.svg" alt="profile">
                    <p>Profile</p>
                </div>
            </RouterLink>

        </div>
    </div>
        
</template>

<style scoped></style>
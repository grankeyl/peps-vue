<script setup lang="ts">
const name = 'EarnView';
</script>

<template>

<div class="earn">
	<div class="earn_inner">

		<div class="upgrades_section earn_limited">
			<div class="upgrades_section_title special_sp">
				<div class="skeleton text">
					<h4>Limited task</h4>
				</div>
				<div
					style="overflow: initial"
					class="special_spanner upgrades_section_skins_item_left_info_title"
				>
					<span
						style="border-radius: 6px"
						id="limited_task_time"
						>6d 2h</span
					>
				</div>
			</div>

			<div class="upgrades_section_content">
				<div
					class="earn_limited_task upgrades_section_skins_item skeleton block"
					id="invite_frien_limited_js"
				>
					<div class="upgrades_section_skins_item_left">
						<div class="upgrades_section_skins_item_left_skin rare">
							<img src="./../assets/img/pepsi.svg" alt="money" />
						</div>

						<div class="upgrades_section_skins_item_left_info">
							<div class="upgrades_section_skins_item_left_info_title">
								<h4>Peps frienship</h4>
							</div>
							<div
								class="upgrades_section_skins_item_left_info_earn upgrades_section_skins_item_left_info_earn_d"
							>
								<p>
									Limited skin and 2,500 $PEPS
								</p>
							</div>
						</div>

						<div class="upgrades_section_skins_item_right_upgrade">
							<svg
								style="margin-left: -40px"
								width="22"
								height="22"
								viewBox="0 0 22 22"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M7.75 11L9.91667 13.1667L14.25 8.83333M1.25 11C1.25 12.2804 1.50219 13.5482 1.99217 14.7312C2.48216 15.9141 3.20034 16.9889 4.10571 17.8943C5.01108 18.7997 6.08591 19.5178 7.26884 20.0078C8.45176 20.4978 9.71961 20.75 11 20.75C12.2804 20.75 13.5482 20.4978 14.7312 20.0078C15.9141 19.5178 16.9889 18.7997 17.8943 17.8943C18.7997 16.9889 19.5178 15.9141 20.0078 14.7312C20.4978 13.5482 20.75 12.2804 20.75 11C20.75 9.71961 20.4978 8.45176 20.0078 7.26884C19.5178 6.08591 18.7997 5.01108 17.8943 4.10571C16.9889 3.20034 15.9141 2.48216 14.7312 1.99217C13.5482 1.50219 12.2804 1.25 11 1.25C9.71961 1.25 8.45176 1.50219 7.26884 1.99217C6.08591 2.48216 5.01108 3.20034 4.10571 4.10571C3.20034 5.01108 2.48216 6.08591 1.99217 7.26884C1.50219 8.45176 1.25 9.71961 1.25 11Z"
									stroke="#65E262"
									stroke-width="1.52941"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="upgrades_section earn_limited">
			<div class="upgrades_section_title skeleton text">
				<h4>Peps challenge</h4>
			</div>

			<div class="earn_challenges_block skeleton block">
				<div class="earn_challenges_block_inner">
					<div class="earn_challenges_block_top">
						<div class="earn_challenges_block_top_block">
							<img src="./../assets/img/money_four.svg" alt="money" />
						</div>
						<div class="earn_challenges_block_top_texts">
							<div class="earn_challenges_block_top_texts_title">
								<h4
									style="
										white-space: nowrap;
										overflow: hidden;
										text-overflow: ellipsis;
										max-width: 122px;
									"
								>
									Invite 10 friens
								</h4>
							</div>
							<div class="earn_challenges_block_top_texts_description">
								<p>
									Get 10,000 $PEPS
								</p>
							</div>
						</div>
						<div class="earn_challenges_block_top_spanner">
							<img src="./../assets/img/money.svg" alt="money" />
							<p>15,000</p>
						</div>
					</div>
					<div class="earn_challenges_block_footer">
						<div class="earn_challenges_block_footer_button">
							<div class="upgrades_section_skins_item_right_upgrade_btn actived">
								<button id="invite_frien_nolimited_js">
									<img
										class="button_loading_img"
										src="./../assets/img/button_loading.svg"
										alt="loading"
									/>
									<p>Invite frien</p>
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="upgrades_section earn_limited earn_tasks">
			<div class="upgrades_section_title skeleton text">
				<h4>Tasks</h4>
			</div>

			<div class="earn_tasks_block skeleton block">
				<div class="earn_tasks_block_item">
					<div class="earn_tasks_block_item_left">
						<div class="earn_tasks_block_item_left_image">
							<!-- <img src="{{ task[2] }}" alt="money" /> -->
						</div>
						<div class="earn_tasks_block_item_left_info">
							<div class="earn_tasks_block_item_left_info_title">
								<h4>1</h4>
							</div>
							<div class="earn_tasks_block_item_left_info_earn">
								<p>+10 $PEPS</p>
							</div>
						</div>
					</div>
					<div class="earn_tasks_block_item_right">
						<button
							class="earn_tasks_block_item_right_button"
						>
							<img
								class="button_loading_img"
								src="./../assets/img/button_loading.svg"
								alt="loading"
							/>
							<svg
								width="17"
								height="17"
								viewBox="0 0 17 17"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M6 8.5L7.66667 10.1667L11 6.83333M1 8.5C1 9.48491 1.19399 10.4602 1.5709 11.3701C1.94781 12.2801 2.50026 13.1069 3.1967 13.8033C3.89314 14.4997 4.71993 15.0522 5.62987 15.4291C6.53982 15.806 7.51509 16 8.5 16C9.48491 16 10.4602 15.806 11.3701 15.4291C12.2801 15.0522 13.1069 14.4997 13.8033 13.8033C14.4997 13.1069 15.0522 12.2801 15.4291 11.3701C15.806 10.4602 16 9.48491 16 8.5C16 7.51509 15.806 6.53982 15.4291 5.62987C15.0522 4.71993 14.4997 3.89314 13.8033 3.1967C13.1069 2.50026 12.2801 1.94781 11.3701 1.5709C10.4602 1.19399 9.48491 1 8.5 1C7.51509 1 6.53982 1.19399 5.62987 1.5709C4.71993 1.94781 3.89314 2.50026 3.1967 3.1967C2.50026 3.89314 1.94781 4.71993 1.5709 5.62987C1.19399 6.53982 1 7.51509 1 8.5Z"
									stroke="#65E262"
									stroke-width="1.17647"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
							<p>Start</p>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

</template>

<style scoped>
    @import '../assets/css/earn.css';
    @import '../assets/css/upgrades.css';
    @import '../assets/css/shop.css';
    @import '../assets/css/profile.css';
</style>
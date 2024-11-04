local player = game.Players.LocalPlayer 
local on_screen = player:WaitForChild("PlayerGui"):WaitForChild("ScreenGui"):WaitForChild("Frame"):WaitForChild("Text")

local function updateDisplay()
	while true do
		for i, item in ipairs(data) do
			on_screen.Text = "Song: '" .. item.song .. "' by: " .. item.artist
			print(i)
			wait(3)
		end
	end
end

coroutine.wrap(updateDisplay)()
package com.nadircare.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.nadircare.app.databinding.ActivityMainBinding
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody
import okhttp3.MultipartBody
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private var selectedFileUri: Uri? = null
    private lateinit var apiService: ApiService

    private val filePickerLauncher = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let {
            selectedFileUri = it
            binding.tvFileName.text = getString(R.string.file_selected, getFileName(it))
            binding.btnUpload.isEnabled = true
            hideError()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Initialize API service
        apiService = RetrofitClient.create()

        setupUI()
    }

    private fun setupUI() {
        binding.btnSelectFile.setOnClickListener {
            openFilePicker()
        }

        binding.btnUpload.setOnClickListener {
            selectedFileUri?.let { uri ->
                uploadFile(uri)
            } ?: run {
                showError(getString(R.string.error_no_file))
            }
        }
    }

    private fun openFilePicker() {
        filePickerLauncher.launch("application/pdf,image/*")
    }

    private fun uploadFile(uri: Uri) {
        showLoading(true)
        hideError()
        hideResults()

        lifecycleScope.launch {
            try {
                // Convert URI to File for multipart upload
                val file = uriToFile(uri)
                
                // Determine media type
                val mediaType = when {
                    file.name.endsWith(".pdf", ignoreCase = true) -> "application/pdf".toMediaTypeOrNull()
                    file.name.endsWith(".jpg", ignoreCase = true) || file.name.endsWith(".jpeg", ignoreCase = true) -> "image/jpeg".toMediaTypeOrNull()
                    file.name.endsWith(".png", ignoreCase = true) -> "image/png".toMediaTypeOrNull()
                    else -> "application/octet-stream".toMediaTypeOrNull()
                }

                val requestFile = RequestBody.create(mediaType, file)
                val multipartBody = MultipartBody.Part.createFormData("file", file.name, requestFile)

                val response = apiService.uploadReport(multipartBody)
                
                if (response.isSuccessful && response.body() != null) {
                    val result = response.body()!!
                    displayResults(result)
                } else {
                    showError(response.message() ?: getString(R.string.error_upload_failed))
                }
                
                showLoading(false)
            } catch (e: Exception) {
                e.printStackTrace()
                showError(getString(R.string.error_upload_failed))
                showLoading(false)
            }
        }
    }

    private fun displayResults(response: AnalysisResponse) {
        val recommendationText = when (response.recommendation) {
            RecommendationType.ADMISSION -> getString(R.string.admission)
            RecommendationType.DOCTOR_VISIT -> getString(R.string.doctor_visit)
            RecommendationType.HOME_MEDICATION -> getString(R.string.home_medication)
        }
        
        showResults(
            recommendation = recommendationText,
            reasoning = response.reasoning ?: "No reasoning provided",
            suggestedActions = response.suggested_actions?.joinToString("\n") ?: "No specific actions suggested"
        )
    }

    private fun uriToFile(uri: Uri): File {
        val inputStream = contentResolver.openInputStream(uri) ?: throw Exception("Cannot open file")
        val fileName = getFileName(uri)
        val file = File(cacheDir, fileName)
        
        FileOutputStream(file).use { output ->
            inputStream.copyTo(output)
        }
        
        return file
    }

    private fun showLoading(show: Boolean) {
        binding.progressBar.visibility = if (show) View.VISIBLE else View.GONE
        binding.tvProgressText.visibility = if (show) View.VISIBLE else View.GONE
        binding.btnUpload.isEnabled = !show
        binding.btnSelectFile.isEnabled = !show
    }

    private fun showResults(recommendation: String, reasoning: String, suggestedActions: String) {
        binding.cardResults.visibility = View.VISIBLE
        binding.tvRecommendationType.text = recommendation
        binding.tvReasoning.text = reasoning
        binding.tvSuggestedActions.text = suggestedActions
        
        // Set icon and color based on recommendation type
        when {
            recommendation.contains("Admission", ignoreCase = true) -> {
                binding.ivRecommendationIcon.setColorFilter(getColor(R.color.error))
            }
            recommendation.contains("Doctor", ignoreCase = true) -> {
                binding.ivRecommendationIcon.setColorFilter(getColor(R.color.warning))
            }
            recommendation.contains("Home", ignoreCase = true) -> {
                binding.ivRecommendationIcon.setColorFilter(getColor(R.color.success))
            }
        }
    }

    private fun hideResults() {
        binding.cardResults.visibility = View.GONE
    }

    private fun showError(message: String) {
        binding.cardError.visibility = View.VISIBLE
        binding.tvError.text = message
    }

    private fun hideError() {
        binding.cardError.visibility = View.GONE
    }

    private fun getFileName(uri: Uri): String {
        var result: String? = null
        if (uri.scheme == "content") {
            val cursor = contentResolver.query(uri, null, null, null, null)
            cursor?.use {
                if (it.moveToFirst()) {
                    val nameIndex = it.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
                    if (nameIndex >= 0) {
                        result = it.getString(nameIndex)
                    }
                }
            }
        }
        if (result == null) {
            result = uri.path
            val cut = result?.lastIndexOf('/')
            if (cut != -1) {
                result = result?.substring(cut!! + 1)
            }
        }
        return result ?: "report_${System.currentTimeMillis()}.pdf"
    }
}

